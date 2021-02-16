package com.mingzzc.redis;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.concurrent.TimeUnit;


@Controller
public class Redis {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    public Object get(String key){
        return stringRedisTemplate.opsForValue().get(key);
    }

    public void set(String key,String value,long timeout){
        stringRedisTemplate.opsForValue().set(key, value, timeout, TimeUnit.SECONDS);
    }
}
