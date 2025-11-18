package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.CreateInvitationRequest;
import com.babykeke.backend.dto.request.JoinFamilyRequest;
import com.babykeke.backend.dto.response.BabyDTO;
import com.babykeke.backend.dto.response.InvitationDTO;
import com.babykeke.backend.entity.*;
import com.babykeke.backend.exception.BusinessException;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyFamilyRepository;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.InvitationRepository;
import com.babykeke.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * 邀请码服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class InvitationService {

    private final InvitationRepository invitationRepository;
    private final BabyRepository babyRepository;
    private final BabyFamilyRepository babyFamilyRepository;
    private final UserRepository userRepository;

    /**
     * 创建邀请码
     */
    @Transactional
    public InvitationDTO createInvitation(Integer babyId, CreateInvitationRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        // 生成邀请码
        String inviteCode = generateInviteCode();

        Invitation invitation = new Invitation();
        invitation.setBaby(baby);
        invitation.setInviteCode(inviteCode);
        invitation.setCreatedBy(userId);
        invitation.setExpireAt(LocalDateTime.now().plusDays(request.getValidDays()));
        invitation.setStatus(InvitationStatus.active);

        invitation = invitationRepository.save(invitation);

        log.info("创建邀请码成功: babyId={}, inviteCode={}", babyId, inviteCode);

        return convertToDTO(invitation);
    }

    /**
     * 获取宝宝的邀请码列表
     */
    public List<InvitationDTO> getInvitations(Integer babyId) {
        List<Invitation> invitations = invitationRepository.findByBabyId(babyId);

        // 自动更新过期状态
        LocalDateTime now = LocalDateTime.now();
        invitations.forEach(inv -> {
            if (inv.getStatus() == InvitationStatus.active && inv.getExpireAt().isBefore(now)) {
                inv.setStatus(InvitationStatus.expired);
                invitationRepository.save(inv);
            }
        });

        return invitations.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * 通过邀请码加入家庭
     */
    @Transactional
    public BabyDTO joinFamily(JoinFamilyRequest request, Integer userId) {
        // 查找邀请码
        Invitation invitation = invitationRepository.findByInviteCode(request.getInviteCode())
                .orElseThrow(() -> new BusinessException("邀请码不存在"));

        // 验证邀请码状态
        if (invitation.getStatus() != InvitationStatus.active) {
            throw new BusinessException("邀请码已失效");
        }

        // 验证是否过期
        if (invitation.getExpireAt().isBefore(LocalDateTime.now())) {
            invitation.setStatus(InvitationStatus.expired);
            invitationRepository.save(invitation);
            throw new BusinessException("邀请码已过期");
        }

        Baby baby = invitation.getBaby();

        // 检查是否已经是家庭成员
        if (babyFamilyRepository.existsByBabyIdAndUserId(baby.getId(), userId)) {
            throw new BusinessException("您已经是该宝宝的家庭成员");
        }

        // 添加家庭成员
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("用户不存在"));

        BabyFamily babyFamily = new BabyFamily();
        babyFamily.setBaby(baby);
        babyFamily.setUser(user);
        babyFamily.setRelation(request.getRelation());
        babyFamily.setRelationDisplay(request.getRelationDisplay());
        babyFamily.setIsAdmin(0);

        babyFamilyRepository.save(babyFamily);

        // 更新邀请码状态
        invitation.setStatus(InvitationStatus.used);
        invitation.setUsedBy(userId);
        invitation.setUsedAt(LocalDateTime.now());
        invitationRepository.save(invitation);

        log.info("通过邀请码加入家庭成功: babyId={}, userId={}, inviteCode={}",
                baby.getId(), userId, request.getInviteCode());

        // 返回宝宝信息
        BabyDTO dto = new BabyDTO();
        dto.setId(baby.getId());
        dto.setName(baby.getName());
        dto.setNickname(baby.getNickname());
        dto.setGender(baby.getGender());
        dto.setBirthday(baby.getBirthday());
        dto.setBirthWeight(baby.getBirthWeight());
        dto.setBirthHeight(baby.getBirthHeight());
        dto.setNotes(baby.getNotes());
        dto.setCreatedBy(baby.getCreatedBy());
        dto.setCreatedAt(baby.getCreatedAt());
        dto.setUpdatedAt(baby.getUpdatedAt());
        dto.setRelation(babyFamily.getRelation());
        dto.setRelationDisplay(babyFamily.getRelationDisplay());
        dto.setIsAdmin(babyFamily.getIsAdmin());

        return dto;
    }

    /**
     * 删除邀请码
     */
    @Transactional
    public void deleteInvitation(Integer babyId, Integer invitationId) {
        Invitation invitation = invitationRepository.findById(invitationId)
                .orElseThrow(() -> new ResourceNotFoundException("邀请码不存在"));

        if (!invitation.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("邀请码不存在");
        }

        invitationRepository.delete(invitation);

        log.info("删除邀请码成功: babyId={}, invitationId={}", babyId, invitationId);
    }

    /**
     * 生成邀请码
     */
    private String generateInviteCode() {
        return UUID.randomUUID().toString().replace("-", "").substring(0, 16).toUpperCase();
    }

    /**
     * 转换为 DTO
     */
    private InvitationDTO convertToDTO(Invitation invitation) {
        InvitationDTO dto = new InvitationDTO();
        dto.setId(invitation.getId());
        dto.setBabyId(invitation.getBaby().getId());
        dto.setBabyName(invitation.getBaby().getName());
        dto.setInviteCode(invitation.getInviteCode());
        dto.setCreatedBy(invitation.getCreatedBy());
        dto.setExpireAt(invitation.getExpireAt());
        dto.setStatus(invitation.getStatus());
        dto.setUsedBy(invitation.getUsedBy());
        dto.setUsedAt(invitation.getUsedAt());
        dto.setCreatedAt(invitation.getCreatedAt());
        return dto;
    }
}
