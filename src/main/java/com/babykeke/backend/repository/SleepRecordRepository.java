package com.babykeke.backend.repository;

import com.babykeke.backend.entity.SleepRecord;
import com.babykeke.backend.entity.SleepStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 睡眠记录 Repository
 */
@Repository
public interface SleepRecordRepository extends JpaRepository<SleepRecord, Integer> {

    /**
     * 分页查询宝宝的睡眠记录
     */
    @Query("SELECT sr FROM SleepRecord sr WHERE sr.baby.id = :babyId ORDER BY sr.startTime DESC")
    Page<SleepRecord> findByBabyId(@Param("babyId") Integer babyId, Pageable pageable);

    /**
     * 按时间范围查询睡眠记录
     */
    @Query("SELECT sr FROM SleepRecord sr WHERE sr.baby.id = :babyId AND sr.startTime BETWEEN :startTime AND :endTime ORDER BY sr.startTime DESC")
    List<SleepRecord> findByBabyIdAndTimeRange(@Param("babyId") Integer babyId,
                                                @Param("startTime") LocalDateTime startTime,
                                                @Param("endTime") LocalDateTime endTime);

    /**
     * 查找进行中的睡眠记录
     */
    @Query("SELECT sr FROM SleepRecord sr WHERE sr.baby.id = :babyId AND sr.status = :status")
    Optional<SleepRecord> findInProgressByBabyId(@Param("babyId") Integer babyId, @Param("status") SleepStatus status);
}
