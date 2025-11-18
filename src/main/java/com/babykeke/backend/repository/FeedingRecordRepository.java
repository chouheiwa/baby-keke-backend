package com.babykeke.backend.repository;

import com.babykeke.backend.entity.FeedingRecord;
import com.babykeke.backend.entity.FeedingType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 喂养记录 Repository
 */
@Repository
public interface FeedingRecordRepository extends JpaRepository<FeedingRecord, Integer> {

    /**
     * 分页查询宝宝的喂养记录
     */
    @Query("SELECT fr FROM FeedingRecord fr WHERE fr.baby.id = :babyId ORDER BY fr.startTime DESC")
    Page<FeedingRecord> findByBabyId(@Param("babyId") Integer babyId, Pageable pageable);

    /**
     * 按类型和时间范围查询喂养记录
     */
    @Query("SELECT fr FROM FeedingRecord fr WHERE fr.baby.id = :babyId AND fr.feedingType = :feedingType AND fr.startTime BETWEEN :startTime AND :endTime ORDER BY fr.startTime DESC")
    List<FeedingRecord> findByBabyIdAndTypeAndTimeRange(@Param("babyId") Integer babyId,
                                                         @Param("feedingType") FeedingType feedingType,
                                                         @Param("startTime") LocalDateTime startTime,
                                                         @Param("endTime") LocalDateTime endTime);

    /**
     * 查询最近的喂养记录
     */
    @Query("SELECT fr FROM FeedingRecord fr WHERE fr.baby.id = :babyId ORDER BY fr.startTime DESC LIMIT 1")
    FeedingRecord findLatestByBabyId(@Param("babyId") Integer babyId);
}
