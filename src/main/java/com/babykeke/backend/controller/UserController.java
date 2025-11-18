package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.UpdateUserRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.UserDTO;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

/**
 * 用户控制器
 */
@Slf4j
@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * 获取当前用户信息
     */
    @GetMapping("/me")
    public ApiResponse<UserDTO> getCurrentUser() {
        Integer userId = CurrentUser.getUserId();
        UserDTO user = userService.getUserInfo(userId);
        return ApiResponse.success(user);
    }

    /**
     * 更新当前用户信息
     */
    @PutMapping("/me")
    public ApiResponse<UserDTO> updateCurrentUser(@Valid @RequestBody UpdateUserRequest request) {
        Integer userId = CurrentUser.getUserId();
        UserDTO user = userService.updateUserInfo(userId, request);
        return ApiResponse.success("更新用户信息成功", user);
    }
}
