package com.mingzzc.controller;

import com.alibaba.fastjson.JSONObject;
import com.mingzzc.dao.Book;
import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.User;
import com.mingzzc.mapper.BookMapperImpl;
import com.mingzzc.mapper.UserMapperImpl;
import com.mingzzc.redis.Redis;
import com.mingzzc.util.ResultJson;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.util.DigestUtils;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.*;


@RestController
@RequestMapping("/api")
public class Api {

    BookMapperImpl bookImpl;
    List<Book> books;
    List<BookBrief> bookBriefs;

    @Autowired
    UserMapperImpl userImpl;

    @Autowired
    Redis redis;

    //数据库插入操作 临时


    @Autowired
    Api(BookMapperImpl impl){
        this.bookImpl = impl;
        this.books = impl.getBooks();
        bookBriefs = new ArrayList<BookBrief>(books.size());
        for(Book b:this.books) {
            bookBriefs.add(new BookBrief(b));
        }
    }

    @ResponseBody
    @GetMapping("/hello")
    public String helloWorld(){
        return "hello world";
    }

    @ResponseBody
    @CrossOrigin(origins = "*")
    @GetMapping("/book/{id}")
    public Book getBooksById(@PathVariable("id") int id){//区分pathVariable RequestParam
        Book b = bookImpl.getBooksById(id);
        System.out.println(b);
        return b;
    }

    //解决跨域问题
    @CrossOrigin(origins = "*")
    @GetMapping("/books")
    public List getAllBooks(@RequestParam("num") int num) {
        System.out.println(num);
        if(num>this.bookBriefs.size())num=this.bookBriefs.size();
        return this.bookBriefs.subList(0,num);
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/register")
    public boolean register(User user){
        System.out.println(user);
        user.setPassword(DigestUtils.md5DigestAsHex(user.getPassword().getBytes()));
        int res = userImpl.addUser(user);
        if(res==1) {
            redis.set("recommend"+user.getUsername(),"",-1);
            return true;
        }
        return false;
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/login")
    public ResultJson<JSONObject> login(User user){
        System.out.println(user);
        user.setPassword(DigestUtils.md5DigestAsHex(user.getPassword().getBytes()));
        User res = userImpl.selectUserByUser(user.getUsername());
        JSONObject result = new JSONObject();
        if(res!=null&&res.getPassword().equals(user.getPassword())){
            result.put("msg","yes");
            String te = user.getUsername()+new Date().getTime();
            String token = DigestUtils.md5DigestAsHex(te.getBytes());
            user.setId(userImpl.getIdByUsername(user.getUsername()));
            redis.set(token, String.valueOf(user.getId()), 3600);
            result.put("token",token);
        }
        else{
            result.put("msg","no");
        }
        return new ResultJson<JSONObject>(200,"success",result);
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/search")
    public JSONObject search(String key,int page,int pagesize){
        System.out.println(key+" "+page+" "+pagesize);
        JSONObject result= new JSONObject();
        List<BookBrief> lists = bookImpl.getBookByKey(key);
        List<BookBrief> te = lists.subList((page-1)*pagesize,Math.min(page*pagesize,lists.size()));
        result.put("data",te);
        result.put("num",lists.size());
        return result;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/tag")
    public JSONObject searchTag(String key,int page,int pagesize){
        JSONObject result= new JSONObject();
        List<BookBrief> lists = bookImpl.getBookByTag(key);
        List<BookBrief> te = lists.subList((page-1)*pagesize,Math.min(page*pagesize,lists.size()));
        result.put("data",te);
        result.put("num",lists.size());
        return result;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/labels")
    public List<String> getLabels(){
        return bookImpl.getLabels();
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/edit")
    public boolean edit(Book book){
        System.out.println(book);
        return bookImpl.edit(book);
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/add")
    public boolean addBook(Book book){
        System.out.println(book);
        return bookImpl.addBook(book);
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/delete")
    public boolean deleteBook(int id){
        return bookImpl.deleteBook(id);
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/getbooklabels")
    public List<String> getBookLabels(int id){
        return bookImpl.getLabelsById(id);
    }
}
