package com.mingzzc.mapper;

import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.User;
import com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserMapperImpl implements UserMapper{

    @Autowired
    private UserMapper mapper;

    @Override
    public int addUser(User user) {
        int res=0;
        try {
            res = mapper.addUser(user);
        }
        catch (Exception e){
            res = 0;
        }
        return res;
    }

    @Override
    public User selectUserByUser(String username) {
        return mapper.selectUserByUser(username);
    }

    @Override
    public int getIdByUsername(String username) {
        return mapper.getIdByUsername(username);
    }
}
