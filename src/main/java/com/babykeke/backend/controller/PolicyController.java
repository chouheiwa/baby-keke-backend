package com.babykeke.backend.controller;

import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.PolicyDTO;
import com.babykeke.backend.entity.PolicyStatus;
import com.babykeke.backend.entity.PolicyType;
import com.babykeke.backend.service.PolicyService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 政策协议控制器
 */
@Slf4j
@RestController
@RequestMapping("/policies")
@RequiredArgsConstructor
public class PolicyController {

    private final PolicyService policyService;

    /**
     * 获取最新发布的政策（服务条款或隐私政策）
     */
    @GetMapping("/latest")
    public ApiResponse<PolicyDTO> getLatestPolicy(@RequestParam PolicyType type,
                                                  @RequestParam(required = false) String locale) {
        PolicyDTO policy = policyService.getLatestPolicy(type, locale);
        return ApiResponse.success(policy);
    }

    /**
     * 获取政策列表
     */
    @GetMapping
    public ApiResponse<List<PolicyDTO>> getPolicies(@RequestParam PolicyType type,
                                                    @RequestParam(required = false) String locale,
                                                    @RequestParam(required = false) PolicyStatus status) {
        List<PolicyDTO> policies = policyService.getPolicies(type, locale, status);
        return ApiResponse.success(policies);
    }

    /**
     * 根据版本获取政策
     */
    @GetMapping("/version/{version}")
    public ApiResponse<PolicyDTO> getPolicyByVersion(@RequestParam PolicyType type,
                                                     @PathVariable String version,
                                                     @RequestParam(required = false) String locale) {
        PolicyDTO policy = policyService.getPolicyByVersion(type, version, locale);
        return ApiResponse.success(policy);
    }
}
