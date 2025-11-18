package com.babykeke.backend.repository;

import com.babykeke.backend.entity.Baby;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 宝宝 Repository
 */
@Repository
public interface BabyRepository extends JpaRepository<Baby, Integer> {

    /**
     * 根据创建人查找宝宝列表
     */
    List<Baby> findByCreatedBy(Integer createdBy);
}
