package com.babykeke.backend.security;

import com.babykeke.backend.entity.User;
import com.babykeke.backend.exception.UnauthorizedException;
import com.babykeke.backend.repository.UserRepository;
import com.babykeke.backend.repository.UserSessionRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.time.LocalDateTime;

/**
 * 微信认证拦截器
 * 从请求头中获取 X-Wx-Openid，验证用户身份
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class WeChatAuthInterceptor implements HandlerInterceptor {

    private final UserRepository userRepository;
    private final UserSessionRepository sessionRepository;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // 从请求头获取 openid（微信云托管会自动注入）
        String openid = request.getHeader("X-Wx-Openid");

        if (openid == null || openid.isEmpty()) {
            throw new UnauthorizedException("未找到用户身份信息");
        }

        // 查找用户
        User user = userRepository.findByOpenid(openid)
                .orElseThrow(() -> new UnauthorizedException("用户不存在，请先登录"));

        // 校验登录态是否有效
        boolean isValid = sessionRepository.existsByOpenidAndExpiresAtAfter(openid, LocalDateTime.now());
        if (!isValid) {
            throw new UnauthorizedException("登录态已过期或未登录，请重新登录");
        }

        // 设置当前用户信息到上下文
        CurrentUser.setUserId(user.getId());
        CurrentUser.setOpenid(openid);

        log.debug("认证成功: userId={}, openid={}", user.getId(), openid);

        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // 请求完成后清除用户信息
        CurrentUser.clear();
    }
}
