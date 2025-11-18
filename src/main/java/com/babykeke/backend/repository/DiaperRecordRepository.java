package com.babykeke.backend.repository;

import com.babykeke.backend.entity.DiaperRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 尿布记录 Repository
 */
@Repository
public interface DiaperRecordRepository extends JpaRepository<DiaperRecord, Integer> {

    /**
     * 分页查询宝宝的尿布记录
     */
    @Query("SELECT dr FROM DiaperRecord dr WHERE dr.baby.id = :babyId ORDER BY dr.recordTime DESC")
    Page<DiaperRecord> findByBabyId(@Param("babyId") Integer babyId, Pageable pageable);

    /**
     * 按时间范围查询尿布记录
     */
    @Query("SELECT dr FROM DiaperRecord dr WHERE dr.baby.id = :babyId AND dr.recordTime BETWEEN :startTime AND :endTime ORDER BY dr.recordTime DESC")
    List<DiaperRecord> findByBabyIdAndTimeRange(@Param("babyId") Integer babyId,
                                                 @Param("startTime") LocalDateTime startTime,
                                                 @Param("endTime") LocalDateTime endTime);
}
