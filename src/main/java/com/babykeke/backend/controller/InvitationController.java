package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.CreateInvitationRequest;
import com.babykeke.backend.dto.request.JoinFamilyRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.BabyDTO;
import com.babykeke.backend.dto.response.InvitationDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.InvitationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 邀请码控制器
 */
@Slf4j
@RestController
@RequiredArgsConstructor
public class InvitationController {

    private final InvitationService invitationService;
    private final BabyAccessValidator accessValidator;

    /**
     * 创建邀请码
     */
    @PostMapping("/babies/{babyId}/invitations")
    public ApiResponse<InvitationDTO> createInvitation(@PathVariable Integer babyId,
                                                       @Valid @RequestBody CreateInvitationRequest request) {
        accessValidator.validateAdmin(babyId);
        InvitationDTO invitation = invitationService.createInvitation(babyId, request, CurrentUser.getUserId());
        return ApiResponse.success("创建邀请码成功", invitation);
    }

    /**
     * 获取宝宝的邀请码列表
     */
    @GetMapping("/babies/{babyId}/invitations")
    public ApiResponse<List<InvitationDTO>> getInvitations(@PathVariable Integer babyId) {
        accessValidator.validateAdmin(babyId);
        List<InvitationDTO> invitations = invitationService.getInvitations(babyId);
        return ApiResponse.success(invitations);
    }

    /**
     * 删除邀请码
     */
    @DeleteMapping("/babies/{babyId}/invitations/{invitationId}")
    public ApiResponse<Void> deleteInvitation(@PathVariable Integer babyId,
                                              @PathVariable Integer invitationId) {
        accessValidator.validateAdmin(babyId);
        invitationService.deleteInvitation(babyId, invitationId);
        return ApiResponse.success("删除邀请码成功");
    }

    /**
     * 通过邀请码加入家庭
     */
    @PostMapping("/invitations/join")
    public ApiResponse<BabyDTO> joinFamily(@Valid @RequestBody JoinFamilyRequest request) {
        BabyDTO baby = invitationService.joinFamily(request, CurrentUser.getUserId());
        return ApiResponse.success("加入家庭成功", baby);
    }
}
