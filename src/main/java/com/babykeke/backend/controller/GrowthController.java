package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.CreateGrowthRecordRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.GrowthRecordDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.GrowthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/babies/{babyId}/growth")
@RequiredArgsConstructor
public class GrowthController {

    private final GrowthService growthService;
    private final BabyAccessValidator accessValidator;

    @PostMapping
    public ApiResponse<GrowthRecordDTO> createRecord(@PathVariable Integer babyId,
                                                     @Valid @RequestBody CreateGrowthRecordRequest request) {
        accessValidator.validateAccess(babyId);
        GrowthRecordDTO record = growthService.createRecord(babyId, request, CurrentUser.getUserId());
        return ApiResponse.success("创建成长记录成功", record);
    }

    @GetMapping
    public ApiResponse<Page<GrowthRecordDTO>> getRecords(@PathVariable Integer babyId,
                                                         @RequestParam(defaultValue = "0") int page,
                                                         @RequestParam(defaultValue = "20") int size) {
        accessValidator.validateAccess(babyId);
        return ApiResponse.success(growthService.getRecords(babyId, page, size));
    }

    @DeleteMapping("/{recordId}")
    public ApiResponse<Void> deleteRecord(@PathVariable Integer babyId,
                                         @PathVariable Integer recordId) {
        accessValidator.validateAccess(babyId);
        growthService.deleteRecord(babyId, recordId);
        return ApiResponse.success("删除成长记录成功");
    }
}
