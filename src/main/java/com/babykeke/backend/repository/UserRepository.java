package com.babykeke.backend.repository;

import com.babykeke.backend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 用户 Repository
 */
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

    /**
     * 根据 openid 查找用户
     */
    Optional<User> findByOpenid(String openid);

    /**
     * 检查 openid 是否存在
     */
    boolean existsByOpenid(String openid);
}
