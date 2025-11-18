package com.babykeke.backend.repository;

import com.babykeke.backend.entity.WeChatAccessToken;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

/**
 * 微信Access Token Repository
 */
@Repository
public interface WeChatAccessTokenRepository extends JpaRepository<WeChatAccessToken, Integer> {

    /**
     * 根据 appid 查找 token
     */
    Optional<WeChatAccessToken> findByAppid(String appid);

    /**
     * 查找有效的 token（未过期）
     */
    Optional<WeChatAccessToken> findByAppidAndExpiresAtAfter(String appid, LocalDateTime now);

    /**
     * 删除过期的 token
     */
    void deleteByExpiresAtBefore(LocalDateTime now);
}
