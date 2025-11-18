package com.babykeke.backend.service;

import com.babykeke.backend.dto.response.PolicyDTO;
import com.babykeke.backend.entity.Policy;
import com.babykeke.backend.entity.PolicyStatus;
import com.babykeke.backend.entity.PolicyType;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.PolicyRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 政策协议服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PolicyService {

    private final PolicyRepository policyRepository;

    /**
     * 获取最新发布的政策
     */
    public PolicyDTO getLatestPolicy(PolicyType type, String locale) {
        Policy policy = policyRepository.findLatestPublished(type, locale != null ? locale : "zh-CN")
                .orElseThrow(() -> new ResourceNotFoundException("未找到政策协议"));

        return convertToDTO(policy);
    }

    /**
     * 根据类型和状态获取政策列表
     */
    public List<PolicyDTO> getPolicies(PolicyType type, String locale, PolicyStatus status) {
        String localeStr = locale != null ? locale : "zh-CN";
        PolicyStatus statusFilter = status != null ? status : PolicyStatus.published;

        List<Policy> policies = policyRepository.findByTypeAndLocaleAndStatus(type, localeStr, statusFilter);

        return policies.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * 根据版本获取政策
     */
    public PolicyDTO getPolicyByVersion(PolicyType type, String version, String locale) {
        String localeStr = locale != null ? locale : "zh-CN";

        Policy policy = policyRepository.findByTypeAndVersionAndLocale(type, version, localeStr)
                .orElseThrow(() -> new ResourceNotFoundException("未找到指定版本的政策协议"));

        return convertToDTO(policy);
    }

    /**
     * 转换为 DTO
     */
    private PolicyDTO convertToDTO(Policy policy) {
        PolicyDTO dto = new PolicyDTO();
        dto.setId(policy.getId());
        dto.setType(policy.getType());
        dto.setVersion(policy.getVersion());
        dto.setTitle(policy.getTitle());
        dto.setContent(policy.getContent());
        dto.setFormat(policy.getFormat());
        dto.setLocale(policy.getLocale());
        dto.setStatus(policy.getStatus());
        dto.setEffectiveAt(policy.getEffectiveAt());
        dto.setCreatedAt(policy.getCreatedAt());
        dto.setUpdatedAt(policy.getUpdatedAt());
        return dto;
    }
}
