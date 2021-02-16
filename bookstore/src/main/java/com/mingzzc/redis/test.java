package com.mingzzc.redis;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/redis")
@ResponseBody
public class test {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @PutMapping("/string/put")
    public  void  put(String key , @RequestParam(required = false,defaultValue = "default") String value){
        stringRedisTemplate.opsForValue().set(key, value);
    }

    @GetMapping("/string/get")
    public  Object get(String key){
        return stringRedisTemplate.opsForValue().get(key);
    }
}