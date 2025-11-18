package com.babykeke.backend.exception;

import lombok.Getter;

/**
 * 微信 API 异常
 */
@Getter
public class WeChatApiException extends RuntimeException {

    private final int errcode;
    private final String errmsg;

    public WeChatApiException(int errcode, String errmsg) {
        super(String.format("微信API错误 [%d]: %s", errcode, errmsg));
        this.errcode = errcode;
        this.errmsg = errmsg;
    }
}
