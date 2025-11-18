package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.AddFamilyMemberRequest;
import com.babykeke.backend.dto.request.CreateBabyRequest;
import com.babykeke.backend.dto.request.UpdateBabyRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.BabyDTO;
import com.babykeke.backend.dto.response.FamilyMemberDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.BabyService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 宝宝控制器
 */
@Slf4j
@RestController
@RequestMapping("/babies")
@RequiredArgsConstructor
public class BabyController {

    private final BabyService babyService;
    private final BabyAccessValidator accessValidator;

    /**
     * 创建宝宝
     */
    @PostMapping
    public ApiResponse<BabyDTO> createBaby(@Valid @RequestBody CreateBabyRequest request) {
        Integer userId = CurrentUser.getUserId();
        BabyDTO baby = babyService.createBaby(request, userId);
        return ApiResponse.success("创建宝宝成功", baby);
    }

    /**
     * 获取用户的所有宝宝
     */
    @GetMapping
    public ApiResponse<List<BabyDTO>> getUserBabies() {
        Integer userId = CurrentUser.getUserId();
        List<BabyDTO> babies = babyService.getUserBabies(userId);
        return ApiResponse.success(babies);
    }

    /**
     * 获取宝宝详情
     */
    @GetMapping("/{id}")
    public ApiResponse<BabyDTO> getBabyDetail(@PathVariable Integer id) {
        accessValidator.validateAccess(id);
        Integer userId = CurrentUser.getUserId();
        BabyDTO baby = babyService.getBabyDetail(id, userId);
        return ApiResponse.success(baby);
    }

    /**
     * 更新宝宝信息
     */
    @PutMapping("/{id}")
    public ApiResponse<BabyDTO> updateBaby(@PathVariable Integer id,
                                           @Valid @RequestBody UpdateBabyRequest request) {
        accessValidator.validateAdmin(id);
        Integer userId = CurrentUser.getUserId();
        BabyDTO baby = babyService.updateBaby(id, request, userId);
        return ApiResponse.success("更新宝宝信息成功", baby);
    }

    /**
     * 删除宝宝
     */
    @DeleteMapping("/{id}")
    public ApiResponse<Void> deleteBaby(@PathVariable Integer id) {
        accessValidator.validateAdmin(id);
        babyService.deleteBaby(id);
        return ApiResponse.success("删除宝宝成功");
    }

    /**
     * 获取宝宝的家庭成员列表
     */
    @GetMapping("/{id}/family")
    public ApiResponse<List<FamilyMemberDTO>> getFamilyMembers(@PathVariable Integer id) {
        accessValidator.validateAccess(id);
        List<FamilyMemberDTO> members = babyService.getFamilyMembers(id);
        return ApiResponse.success(members);
    }

    /**
     * 添加家庭成员
     */
    @PostMapping("/{id}/family")
    public ApiResponse<FamilyMemberDTO> addFamilyMember(@PathVariable Integer id,
                                                        @Valid @RequestBody AddFamilyMemberRequest request) {
        accessValidator.validateAdmin(id);
        FamilyMemberDTO member = babyService.addFamilyMember(id, request);
        return ApiResponse.success("添加家庭成员成功", member);
    }

    /**
     * 移除家庭成员
     */
    @DeleteMapping("/{id}/family/{userId}")
    public ApiResponse<Void> removeFamilyMember(@PathVariable Integer id,
                                                @PathVariable Integer userId) {
        accessValidator.validateAdmin(id);
        babyService.removeFamilyMember(id, userId);
        return ApiResponse.success("移除家庭成员成功");
    }

    /**
     * 更新家庭成员角色
     */
    @PutMapping("/{id}/family/{userId}")
    public ApiResponse<FamilyMemberDTO> updateFamilyMemberRole(@PathVariable Integer id,
                                                               @PathVariable Integer userId,
                                                               @RequestParam(required = false) String relation,
                                                               @RequestParam(required = false) String relationDisplay,
                                                               @RequestParam(required = false) Integer isAdmin) {
        accessValidator.validateAdmin(id);
        FamilyMemberDTO member = babyService.updateFamilyMemberRole(id, userId, relation, relationDisplay, isAdmin);
        return ApiResponse.success("更新家庭成员角色成功", member);
    }
}
