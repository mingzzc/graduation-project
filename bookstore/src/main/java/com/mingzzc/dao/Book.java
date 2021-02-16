package com.mingzzc.dao;

import java.io.Serializable;


public class Book implements Serializable {
    private String id;
    private String title;
    private String picture;
    private String star;
    private String author;
    private String pub_site;
    private String pub_time;
    private int pages;
    private String bind;
    private String price;
    private String info;
    private String book_desc;
    private String author_desc;
    private String isbn;

    public Book() {
    }

    @Override
    public String toString() {
        return "Book{" +
                "id='" + id + '\'' +
                ", title='" + title + '\'' +
                ", picture='" + picture + '\'' +
                ", star='" + star + '\'' +
                ", author='" + author + '\'' +
                ", pub_site='" + pub_site + '\'' +
                ", pub_time='" + pub_time + '\'' +
                ", pages=" + pages +
                ", bind='" + bind + '\'' +
                ", price='" + price + '\'' +
                ", info='" + info + '\'' +
                ", book_desc='" + book_desc + '\'' +
                ", author_desc='" + author_desc + '\'' +
                ", isbn='" + isbn + '\'' +
                '}';
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getPicture() {
        return picture;
    }

    public void setPicture(String picture) {
        this.picture = picture;
    }

    public String getStar() {
        return star;
    }

    public void setStar(String star) {
        this.star = star;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getPub_site() {
        return pub_site;
    }

    public void setPub_site(String pub_site) {
        this.pub_site = pub_site;
    }

    public String getPub_time() {
        return pub_time;
    }

    public void setPub_time(String pub_time) {
        this.pub_time = pub_time;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    public String getBind() {
        return bind;
    }

    public void setBind(String bind) {
        this.bind = bind;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getInfo() {
        if(this.info==null)this.info=this.author+"?????????/ "+this.pub_site+"/ "+this.pub_time+"/ "+this.price;
        return info;
    }

    /*public void setInfo(String info) {
        this.info = info;
    }*/

    public String getBook_desc() {
        return book_desc;
    }

    public void setBook_desc(String book_desc) {
        this.book_desc = book_desc;
    }

    public String getAuthor_desc() {
        return author_desc;
    }

    public void setAuthor_desc(String author_desc) {
        this.author_desc = author_desc;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }
}
