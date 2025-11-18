package com.babykeke.backend.exception;

/**
 * 禁止访问异常
 */
public class ForbiddenException extends RuntimeException {

    public ForbiddenException(String message) {
        super(message);
    }
}
