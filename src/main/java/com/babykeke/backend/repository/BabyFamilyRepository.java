package com.babykeke.backend.repository;

import com.babykeke.backend.entity.BabyFamily;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 宝宝家庭成员关系 Repository
 */
@Repository
public interface BabyFamilyRepository extends JpaRepository<BabyFamily, Integer> {

    /**
     * 查找用户的所有宝宝关系
     */
    @Query("SELECT bf FROM BabyFamily bf WHERE bf.user.id = :userId")
    List<BabyFamily> findByUserId(@Param("userId") Integer userId);

    /**
     * 查找宝宝的所有家庭成员
     */
    @Query("SELECT bf FROM BabyFamily bf WHERE bf.baby.id = :babyId")
    List<BabyFamily> findByBabyId(@Param("babyId") Integer babyId);

    /**
     * 查找用户和宝宝的关系
     */
    @Query("SELECT bf FROM BabyFamily bf WHERE bf.baby.id = :babyId AND bf.user.id = :userId")
    Optional<BabyFamily> findByBabyIdAndUserId(@Param("babyId") Integer babyId, @Param("userId") Integer userId);

    /**
     * 检查用户是否是宝宝的家庭成员
     */
    @Query("SELECT COUNT(bf) > 0 FROM BabyFamily bf WHERE bf.baby.id = :babyId AND bf.user.id = :userId")
    boolean existsByBabyIdAndUserId(@Param("babyId") Integer babyId, @Param("userId") Integer userId);

    /**
     * 检查用户是否是宝宝的管理员
     */
    @Query("SELECT COUNT(bf) > 0 FROM BabyFamily bf WHERE bf.baby.id = :babyId AND bf.user.id = :userId AND bf.isAdmin = 1")
    boolean isAdmin(@Param("babyId") Integer babyId, @Param("userId") Integer userId);
}
