package com.babykeke.backend.repository;

import com.babykeke.backend.entity.Invitation;
import com.babykeke.backend.entity.InvitationStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 邀请码 Repository
 */
@Repository
public interface InvitationRepository extends JpaRepository<Invitation, Integer> {

    /**
     * 根据邀请码查找
     */
    Optional<Invitation> findByInviteCode(String inviteCode);

    /**
     * 查找宝宝的所有邀请码
     */
    @Query("SELECT i FROM Invitation i WHERE i.baby.id = :babyId")
    List<Invitation> findByBabyId(@Param("babyId") Integer babyId);

    /**
     * 查找宝宝的活跃邀请码
     */
    @Query("SELECT i FROM Invitation i WHERE i.baby.id = :babyId AND i.status = :status")
    List<Invitation> findByBabyIdAndStatus(@Param("babyId") Integer babyId, @Param("status") InvitationStatus status);
}
