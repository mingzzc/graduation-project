package com.mingzzc.mapper;

import com.mingzzc.dao.Book;
import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookMapperImpl implements BookMapper{

    @Autowired
    private BookMapper mapper;


    @Override
    public List<Book> getBooks() {
        return mapper.getBooks();
    }

    @Override
    public Book getBooksById(int id) {
        return mapper.getBooksById(id);
    }

    @Override
    public List<BookBrief> getBookByKey(String key) {
        return mapper.getBookByKey(key);
    }

    @Override
    public List<BookBrief> getBookByTag(String tag) {
        return mapper.getBookByTag(tag);
    }

    @Override
    public List<String> getLabels() {
        return mapper.getLabels();
    }

    @Override
    public List<String> getLabelsById(int id) {
        return mapper.getLabelsById(id);
    }

    @Override
    public List<BookBrief> getRecommend(String key) {
        return mapper.getRecommend(key);
    }

    @Override
    public Boolean edit(Book book) {
        return mapper.edit(book);
    }

    @Override
    public Boolean addBook(Book book) {
        return mapper.addBook(book);
    }

    @Override
    public Boolean deleteBook(int id) {
        return mapper.deleteBook(id);
    }
}
