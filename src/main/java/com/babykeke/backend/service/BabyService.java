package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.AddFamilyMemberRequest;
import com.babykeke.backend.dto.request.CreateBabyRequest;
import com.babykeke.backend.dto.request.UpdateBabyRequest;
import com.babykeke.backend.dto.response.BabyDTO;
import com.babykeke.backend.dto.response.FamilyMemberDTO;
import com.babykeke.backend.entity.Baby;
import com.babykeke.backend.entity.BabyFamily;
import com.babykeke.backend.entity.User;
import com.babykeke.backend.exception.BusinessException;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyFamilyRepository;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 宝宝服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class BabyService {

    private final BabyRepository babyRepository;
    private final BabyFamilyRepository babyFamilyRepository;
    private final UserRepository userRepository;

    /**
     * 创建宝宝
     */
    @Transactional
    public BabyDTO createBaby(CreateBabyRequest request, Integer userId) {
        // 创建宝宝
        Baby baby = new Baby();
        baby.setName(request.getName());
        baby.setNickname(request.getNickname());
        baby.setGender(request.getGender());
        baby.setBirthday(request.getBirthday());
        baby.setBirthWeight(request.getBirthWeight());
        baby.setBirthHeight(request.getBirthHeight());
        baby.setNotes(request.getNotes());
        baby.setCreatedBy(userId);

        baby = babyRepository.save(baby);

        // 创建家庭成员关系（创建人默认为管理员）
        BabyFamily babyFamily = new BabyFamily();
        babyFamily.setBaby(baby);
        babyFamily.setUser(userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("用户不存在")));
        babyFamily.setRelation(request.getRelation());
        babyFamily.setRelationDisplay(request.getRelationDisplay());
        babyFamily.setIsAdmin(1); // 创建人默认为管理员

        babyFamilyRepository.save(babyFamily);

        log.info("创建宝宝成功: babyId={}, userId={}", baby.getId(), userId);

        return convertToDTO(baby, babyFamily);
    }

    /**
     * 获取用户的所有宝宝
     */
    public List<BabyDTO> getUserBabies(Integer userId) {
        List<BabyFamily> babyFamilies = babyFamilyRepository.findByUserId(userId);

        return babyFamilies.stream()
                .map(bf -> convertToDTO(bf.getBaby(), bf))
                .collect(Collectors.toList());
    }

    /**
     * 获取宝宝详情
     */
    public BabyDTO getBabyDetail(Integer babyId, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        BabyFamily babyFamily = babyFamilyRepository.findByBabyIdAndUserId(babyId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("您不是该宝宝的家庭成员"));

        return convertToDTO(baby, babyFamily);
    }

    /**
     * 更新宝宝信息
     */
    @Transactional
    public BabyDTO updateBaby(Integer babyId, UpdateBabyRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        // 只更新非空字段
        if (request.getName() != null) {
            baby.setName(request.getName());
        }
        if (request.getNickname() != null) {
            baby.setNickname(request.getNickname());
        }
        if (request.getGender() != null) {
            baby.setGender(request.getGender());
        }
        if (request.getBirthday() != null) {
            baby.setBirthday(request.getBirthday());
        }
        if (request.getBirthWeight() != null) {
            baby.setBirthWeight(request.getBirthWeight());
        }
        if (request.getBirthHeight() != null) {
            baby.setBirthHeight(request.getBirthHeight());
        }
        if (request.getNotes() != null) {
            baby.setNotes(request.getNotes());
        }

        baby = babyRepository.save(baby);

        BabyFamily babyFamily = babyFamilyRepository.findByBabyIdAndUserId(babyId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("您不是该宝宝的家庭成员"));

        log.info("更新宝宝成功: babyId={}, userId={}", babyId, userId);

        return convertToDTO(baby, babyFamily);
    }

    /**
     * 删除宝宝
     */
    @Transactional
    public void deleteBaby(Integer babyId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        babyRepository.delete(baby);

        log.info("删除宝宝成功: babyId={}", babyId);
    }

    /**
     * 获取宝宝的家庭成员列表
     */
    public List<FamilyMemberDTO> getFamilyMembers(Integer babyId) {
        List<BabyFamily> familyMembers = babyFamilyRepository.findByBabyId(babyId);

        return familyMembers.stream()
                .map(this::convertToFamilyMemberDTO)
                .collect(Collectors.toList());
    }

    /**
     * 添加家庭成员
     */
    @Transactional
    public FamilyMemberDTO addFamilyMember(Integer babyId, AddFamilyMemberRequest request) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("用户不存在"));

        // 检查是否已经是家庭成员
        if (babyFamilyRepository.existsByBabyIdAndUserId(babyId, request.getUserId())) {
            throw new BusinessException("该用户已经是家庭成员");
        }

        BabyFamily babyFamily = new BabyFamily();
        babyFamily.setBaby(baby);
        babyFamily.setUser(user);
        babyFamily.setRelation(request.getRelation());
        babyFamily.setRelationDisplay(request.getRelationDisplay());
        babyFamily.setIsAdmin(request.getIsAdmin());

        babyFamily = babyFamilyRepository.save(babyFamily);

        log.info("添加家庭成员成功: babyId={}, userId={}", babyId, request.getUserId());

        return convertToFamilyMemberDTO(babyFamily);
    }

    /**
     * 移除家庭成员
     */
    @Transactional
    public void removeFamilyMember(Integer babyId, Integer userId) {
        BabyFamily babyFamily = babyFamilyRepository.findByBabyIdAndUserId(babyId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("该用户不是家庭成员"));

        // 不能移除创建人
        if (babyFamily.getBaby().getCreatedBy().equals(userId)) {
            throw new BusinessException("不能移除宝宝创建人");
        }

        babyFamilyRepository.delete(babyFamily);

        log.info("移除家庭成员成功: babyId={}, userId={}", babyId, userId);
    }

    /**
     * 更新家庭成员角色
     */
    @Transactional
    public FamilyMemberDTO updateFamilyMemberRole(Integer babyId, Integer userId, String relation, String relationDisplay, Integer isAdmin) {
        BabyFamily babyFamily = babyFamilyRepository.findByBabyIdAndUserId(babyId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("该用户不是家庭成员"));

        if (relation != null) {
            babyFamily.setRelation(relation);
        }
        if (relationDisplay != null) {
            babyFamily.setRelationDisplay(relationDisplay);
        }
        if (isAdmin != null) {
            babyFamily.setIsAdmin(isAdmin);
        }

        babyFamily = babyFamilyRepository.save(babyFamily);

        log.info("更新家庭成员角色成功: babyId={}, userId={}", babyId, userId);

        return convertToFamilyMemberDTO(babyFamily);
    }

    /**
     * 转换为 DTO
     */
    private BabyDTO convertToDTO(Baby baby, BabyFamily babyFamily) {
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

        // 设置当前用户的角色信息
        if (babyFamily != null) {
            dto.setRelation(babyFamily.getRelation());
            dto.setRelationDisplay(babyFamily.getRelationDisplay());
            dto.setIsAdmin(babyFamily.getIsAdmin());
        }

        return dto;
    }

    /**
     * 转换为家庭成员 DTO
     */
    private FamilyMemberDTO convertToFamilyMemberDTO(BabyFamily babyFamily) {
        FamilyMemberDTO dto = new FamilyMemberDTO();
        dto.setId(babyFamily.getId());
        dto.setUserId(babyFamily.getUser().getId());
        dto.setUserNickname(babyFamily.getUser().getNickname());
        dto.setRelation(babyFamily.getRelation());
        dto.setRelationDisplay(babyFamily.getRelationDisplay());
        dto.setIsAdmin(babyFamily.getIsAdmin());
        dto.setCreatedAt(babyFamily.getCreatedAt());
        return dto;
    }
}
