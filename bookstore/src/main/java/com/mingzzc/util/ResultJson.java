package com.mingzzc.util;

public class ResultJson<T> {
    private int code;
    private String msg;
    private T data;
    /**     * 操作成功     */    public static final ResultJson SUCCESS_RESULT = new ResultJson(0, "操作成功!!!");
    /**     * 系统异常     */    public static final ResultJson SYSTEM_ERROR_RESULT = new ResultJson(1, "系统异常, 请稍后重试!!!");
    /**     * 登录异常     */    public static final ResultJson LOGIN_ERROR_RESULT = new ResultJson(2, "登录信息已失效, 请重新登录!!!");
    /**     * 请求参数异常     */    public static final ResultJson PARAM_ERROR_RESULT = new ResultJson(3, "请求参数异常, 请重试!!!");
    /**     * 操作失败     */    public static final ResultJson FAIL_RESULT = new ResultJson(4, "操作失败, 请重试!!!");

    /**     * 默认错误编码     */    public static final int ERROR = 9;
    public ResultJson() {    }
    public ResultJson(T data) {        this.code = ResultJson.SUCCESS_RESULT.getCode();        this.msg = ResultJson.SUCCESS_RESULT.getMsg();        this.data = data;    }
    public ResultJson(int code, String msg) {        this.code = code;        this.msg = msg;    }
    public ResultJson(int code, String msg, T data) {        this.code = code;        this.msg = msg;        this.data = data;    }
    public ResultJson(ResultJson param, T data) {        this.code = param.getCode();        this.msg = param.getMsg();        this.data = data;    }
    public static <T> ResultJson<T> error(String message) {        return (ResultJson<T>) new ResultJson(ERROR, message);    }
    public static <T> ResultJson<T> data(T data) {        return (ResultJson<T>) new ResultJson(SUCCESS_RESULT, data);    }
    public int getCode() {        return code;    }
    public void setCode(int code) {        this.code = code;    }
    public String getMsg() {        return msg;    }
    public void setMsg(String msg) {        this.msg = msg;    }
    public T getData() {        return data;    }
    public void setData(T data) {        this.data = data;    }
}
