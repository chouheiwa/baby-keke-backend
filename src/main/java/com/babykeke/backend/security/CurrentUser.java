package com.babykeke.backend.security;

import lombok.Data;

/**
 * 当前用户上下文
 */
@Data
public class CurrentUser {

    private static final ThreadLocal<Integer> USER_ID = new ThreadLocal<>();
    private static final ThreadLocal<String> OPENID = new ThreadLocal<>();

    /**
     * 设置当前用户ID
     */
    public static void setUserId(Integer userId) {
        USER_ID.set(userId);
    }

    /**
     * 获取当前用户ID
     */
    public static Integer getUserId() {
        return USER_ID.get();
    }

    /**
     * 设置当前用户OpenID
     */
    public static void setOpenid(String openid) {
        OPENID.set(openid);
    }

    /**
     * 获取当前用户OpenID
     */
    public static String getOpenid() {
        return OPENID.get();
    }

    /**
     * 清除当前用户信息
     */
    public static void clear() {
        USER_ID.remove();
        OPENID.remove();
    }
}
