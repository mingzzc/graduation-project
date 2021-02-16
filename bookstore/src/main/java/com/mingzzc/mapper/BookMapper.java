package com.mingzzc.mapper;

import com.fasterxml.jackson.databind.deser.std.NumberDeserializers;
import com.mingzzc.dao.Book;
import com.mingzzc.dao.BookBrief;
import com.mingzzc.dao.User;
import org.apache.ibatis.annotations.*;

import java.util.List;


@Mapper
public interface BookMapper {
    /*
    $要加@Param
    #不用
     */
    @Select("select * from books where id between 1000000 and 1000900")
    List<Book> getBooks();

    @Select("select * from books where id = #{id}")
    Book getBooksById(int id);

    @Select("select * from books where title like binary '%${key}%'")
    List<BookBrief> getBookByKey(@Param("key")String key);

    @Select("select books.id,books.title,books.info from books,labels,book_labels where books.id=book_labels.book_id and labels.id = book_labels.label_id and labels.label='${tag}'")
    List<BookBrief> getBookByTag(@Param("tag")String tag);

    @Select("select label from labels where id <= 20")
    List<String> getLabels();

    @Select("select labels.label from labels,book_labels where book_labels.book_id=${id} and book_labels.label_id=labels.id")
    List<String> getLabelsById(@Param("id")int id);

    @Select("select id,title,info from books where id in ${key}")
    List<BookBrief> getRecommend(@Param("key")String key);

    @Update("update books set title=#{title},author=#{author},pages=#{pages},bind=#{bind},price=#{price},info=#{info} where id = #{id}")
    Boolean edit(Book book);

    @Insert("insert into books(id,title,author,pages,bind,price) values('8000000',#{title},#{author},#{pages},#{bind},#{price})")
    Boolean addBook(Book book);

    @Delete("delete from books where id = #{id}")
    Boolean deleteBook(int id);
}
