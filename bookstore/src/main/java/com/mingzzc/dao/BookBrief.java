package com.mingzzc.dao;


import java.io.Serializable;

public class BookBrief implements Serializable {
    private String id;
    private String info;
    private String title;
    public BookBrief(Book book){
        this.id = book.getId();
        this.info = book.getInfo();
        this.title = book.getTitle();
    }

    public BookBrief(String id, String info, String title) {
        this.id = id;
        this.info = info;
        this.title = title;
    }

    public BookBrief() {
    }

    @Override
    public String toString() {
        return "BookBrief{" +
                "id='" + id + '\'' +
                ", info='" + info + '\'' +
                '}';
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getInfo() {
        return info;
    }

    public void setInfo(String info) {
        this.info = info;
    }
}
