package com.mingzzc.controller;


import com.mingzzc.dao.Book;
import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.Recommend;
import com.mingzzc.mapper.BookMapperImpl;
import com.mingzzc.redis.Redis;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;


@RestController
@RequestMapping("/redisapi")
public class RedisApi {

    Redis redis;
    BookMapperImpl bookimpl;

    List<Recommend> recommendList;

    @Autowired
    RedisApi(Redis redis, BookMapperImpl bookimpl){
        this.redis = redis;
        this.bookimpl = bookimpl;
        recommendList = new ArrayList<Recommend>();
        String top = (String) redis.get("top");
        System.out.println(top);
        String[] te = top.split(",");
        for(String item:te){
            String[] it = item.split(":");
            recommendList.add(new Recommend(Integer.decode(it[0]),Double.parseDouble(it[1])));
        }
        for(Recommend recommend:recommendList){
            System.out.println(recommend);
        }
    }


    @GetMapping("/getstar")
    public String getStar(@RequestParam("id") int id){
        return (String)redis.get("star"+String.valueOf(id));
    }


    public int getId(String token){
        int id = -1;
        try {
            id = Integer.decode((String)redis.get(token));
        }
        catch (Exception e){

        }
        finally {
            return id;
        }
    }


    @CrossOrigin(origins = "*")
    @GetMapping("/getrecommend")
    public List getRecommend(String token){
        System.out.println("recommend: "+token);
        int id = getId(token);
        int total = 10;
        if(id == -1)return null;
        String re = (String)redis.get("recommend"+String.valueOf(id));
        if(re.equals("")){
            int [] temp = rand(recommendList.size(),total);
            StringBuilder s = new StringBuilder("(");
            for(int i=0;i<total;i++){
                s.append(String.valueOf(recommendList.get(temp[i]).getId()));
                if(i!=total-1)s.append(",");
                else s.append(")");
            }
            return bookimpl.getRecommend(s.toString());
        }
        String[] string = re.split(",");
        List<Recommend> result = new ArrayList<Recommend>();
        for (String s : string) {
            String[] r = s.split(":");
            Recommend recommend = new Recommend();
            recommend.setId(Integer.decode(r[0]));
            recommend.setIndex(Double.parseDouble(r[1]));
            result.add(recommend);
        }
        if (result.size()<total){
            result.addAll(recommendList);
        }
        int [] temp = rand(result.size(),total);
        StringBuilder s = new StringBuilder("(");
        for(int i=0;i<total;i++){
            s.append(String.valueOf(result.get(temp[i]).getId()));
            if(i!=total-1)s.append(",");
            else s.append(")");
        }
        return bookimpl.getRecommend(s.toString());
    }

    public int[] rand(int num,int total){
        int []result = new int[total];
        Random random = new Random();
        Set<Integer> st = new HashSet<Integer>();
        while(st.size()<total){
            st.add(random.nextInt(num));
        }
        int index = 0;
        for(int a:st){
            result[index++]=a;
        }
        return result;
    }
}
