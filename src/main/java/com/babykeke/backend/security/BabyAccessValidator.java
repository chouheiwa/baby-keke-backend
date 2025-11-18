package com.babykeke.backend.security;

import com.babykeke.backend.exception.ForbiddenException;
import com.babykeke.backend.repository.BabyFamilyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * 宝宝访问权限验证器
 */
@Component
@RequiredArgsConstructor
public class BabyAccessValidator {

    private final BabyFamilyRepository babyFamilyRepository;

    /**
     * 验证用户是否有权访问该宝宝的数据
     */
    public void validateAccess(Integer babyId) {
        Integer userId = CurrentUser.getUserId();
        if (userId == null) {
            throw new ForbiddenException("未登录");
        }

        boolean isMember = babyFamilyRepository.existsByBabyIdAndUserId(babyId, userId);
        if (!isMember) {
            throw new ForbiddenException("您没有权限访问此宝宝的信息");
        }
    }

    /**
     * 验证用户是否是该宝宝的管理员
     */
    public void validateAdmin(Integer babyId) {
        Integer userId = CurrentUser.getUserId();
        if (userId == null) {
            throw new ForbiddenException("未登录");
        }

        boolean isAdmin = babyFamilyRepository.isAdmin(babyId, userId);
        if (!isAdmin) {
            throw new ForbiddenException("您没有管理员权限");
        }
    }
}
