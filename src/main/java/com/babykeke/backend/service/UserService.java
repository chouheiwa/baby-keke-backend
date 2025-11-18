package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.UpdateUserRequest;
import com.babykeke.backend.dto.response.UserDTO;
import com.babykeke.backend.entity.User;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    /**
     * 获取用户信息
     */
    public UserDTO getUserInfo(Integer userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("用户不存在"));

        return convertToDTO(user);
    }

    /**
     * 更新用户信息
     */
    @Transactional
    public UserDTO updateUserInfo(Integer userId, UpdateUserRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("用户不存在"));

        if (request.getNickname() != null) {
            user.setNickname(request.getNickname());
        }
        if (request.getPhone() != null) {
            user.setPhone(request.getPhone());
        }

        user = userRepository.save(user);

        log.info("更新用户信息成功: userId={}", userId);

        return convertToDTO(user);
    }

    /**
     * 转换为 DTO
     */
    private UserDTO convertToDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setOpenid(user.getOpenid());
        dto.setNickname(user.getNickname());
        dto.setPhone(user.getPhone());
        dto.setCreatedAt(user.getCreatedAt());
        dto.setUpdatedAt(user.getUpdatedAt());
        return dto;
    }
}
