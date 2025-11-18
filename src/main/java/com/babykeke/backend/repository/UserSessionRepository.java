package com.babykeke.backend.repository;

import com.babykeke.backend.entity.UserSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

/**
 * 用户会话 Repository
 */
@Repository
public interface UserSessionRepository extends JpaRepository<UserSession, Integer> {

    /**
     * 根据 openid 查找会话
     */
    Optional<UserSession> findByOpenid(String openid);

    /**
     * 检查会话是否有效（未过期）
     */
    boolean existsByOpenidAndExpiresAtAfter(String openid, LocalDateTime now);

    /**
     * 删除过期的会话
     */
    void deleteByExpiresAtBefore(LocalDateTime now);
}
