package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.CreateDiaperRecordRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.DiaperRecordDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.DiaperService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/babies/{babyId}/diaper")
@RequiredArgsConstructor
public class DiaperController {

    private final DiaperService diaperService;
    private final BabyAccessValidator accessValidator;

    @PostMapping
    public ApiResponse<DiaperRecordDTO> createRecord(@PathVariable Integer babyId,
                                                     @Valid @RequestBody CreateDiaperRecordRequest request) {
        accessValidator.validateAccess(babyId);
        DiaperRecordDTO record = diaperService.createRecord(babyId, request, CurrentUser.getUserId());
        return ApiResponse.success("创建尿布记录成功", record);
    }

    @GetMapping
    public ApiResponse<Page<DiaperRecordDTO>> getRecords(@PathVariable Integer babyId,
                                                         @RequestParam(defaultValue = "0") int page,
                                                         @RequestParam(defaultValue = "20") int size) {
        accessValidator.validateAccess(babyId);
        return ApiResponse.success(diaperService.getRecords(babyId, page, size));
    }

    @DeleteMapping("/{recordId}")
    public ApiResponse<Void> deleteRecord(@PathVariable Integer babyId,
                                         @PathVariable Integer recordId) {
        accessValidator.validateAccess(babyId);
        diaperService.deleteRecord(babyId, recordId);
        return ApiResponse.success("删除尿布记录成功");
    }
}
