package com.babykeke.backend.controller;

import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.HomeDataDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.HomeService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 首页控制器
 */
@Slf4j
@RestController
@RequestMapping("/home")
@RequiredArgsConstructor
public class HomeController {

    private final HomeService homeService;
    private final BabyAccessValidator accessValidator;

    /**
     * 获取首页聚合数据
     */
    @GetMapping("/babies/{babyId}")
    public ApiResponse<HomeDataDTO> getHomeData(@PathVariable Integer babyId) {
        accessValidator.validateAccess(babyId);
        HomeDataDTO data = homeService.getHomeData(babyId, CurrentUser.getUserId());
        return ApiResponse.success(data);
    }
}
