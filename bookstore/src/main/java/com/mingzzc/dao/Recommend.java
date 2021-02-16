package com.mingzzc.dao;

public class Recommend {
    private int id;
    private double index;

    @Override
    public String toString() {
        return "Recommend{" +
                "id=" + id +
                ", index=" + index +
                '}';
    }

    public Recommend() {
    }

    public Recommend(int id, double index) {
        this.id = id;
        this.index = index;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getIndex() {
        return index;
    }

    public void setIndex(double index) {
        this.index = index;
    }
}
