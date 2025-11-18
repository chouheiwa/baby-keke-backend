package com.babykeke.backend.repository;

import com.babykeke.backend.entity.GrowthRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 成长记录 Repository
 */
@Repository
public interface GrowthRecordRepository extends JpaRepository<GrowthRecord, Integer> {

    /**
     * 分页查询宝宝的成长记录
     */
    @Query("SELECT gr FROM GrowthRecord gr WHERE gr.baby.id = :babyId ORDER BY gr.recordDate DESC")
    Page<GrowthRecord> findByBabyId(@Param("babyId") Integer babyId, Pageable pageable);

    /**
     * 按时间范围查询成长记录
     */
    @Query("SELECT gr FROM GrowthRecord gr WHERE gr.baby.id = :babyId AND gr.recordDate BETWEEN :startDate AND :endDate ORDER BY gr.recordDate ASC")
    List<GrowthRecord> findByBabyIdAndDateRange(@Param("babyId") Integer babyId,
                                                 @Param("startDate") LocalDateTime startDate,
                                                 @Param("endDate") LocalDateTime endDate);

    /**
     * 查询最新的成长记录
     */
    @Query("SELECT gr FROM GrowthRecord gr WHERE gr.baby.id = :babyId ORDER BY gr.recordDate DESC LIMIT 1")
    GrowthRecord findLatestByBabyId(@Param("babyId") Integer babyId);
}
