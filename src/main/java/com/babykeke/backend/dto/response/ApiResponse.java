package com.babykeke.backend.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 统一 API 响应格式
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {

    /**
     * 状态码
     */
    private int code;

    /**
     * 消息
     */
    private String message;

    /**
     * 数据
     */
    private T data;

    /**
     * 时间戳
     */
    private LocalDateTime timestamp;

    public ApiResponse() {
        this.timestamp = LocalDateTime.now();
    }

    public ApiResponse(int code, String message) {
        this();
        this.code = code;
        this.message = message;
    }

    public ApiResponse(int code, String message, T data) {
        this(code, message);
        this.data = data;
    }

    /**
     * 成功响应（无数据）
     */
    public static <T> ApiResponse<T> success() {
        return new ApiResponse<>(200, "操作成功");
    }

    /**
     * 成功响应（有数据）
     */
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(200, "操作成功", data);
    }

    /**
     * 成功响应（自定义消息）
     */
    public static <T> ApiResponse<T> success(String message, T data) {
        return new ApiResponse<>(200, message, data);
    }

    /**
     * 失败响应
     */
    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>(500, message);
    }

    /**
     * 失败响应（自定义状态码）
     */
    public static <T> ApiResponse<T> error(int code, String message) {
        return new ApiResponse<>(code, message);
    }
}
