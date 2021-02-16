package com.mingzzc.mapper;

import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UserMapper {

    @Insert("insert into users(username,password,email) values(#{username},#{password},#{email})")
    public int addUser(User user);

    @Select("select id,username,password,email from users where username=#{username}")
    public User selectUserByUser(String username);

    @Select("select id from users where username=#{username}")
    public int getIdByUsername(String username);
}
