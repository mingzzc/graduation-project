<template>
  <el-card class="book">
    <el-col :span="16">
      <el-card class="book_desc">
        <el-col :span="8">
          <div class="col1">
            <span class="title">{{book.title}}</span>
            <img width="210px" height="300px" :src='"../assets/imgs/tempimg.jpg"'>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="desc">
            <li v-for='(value,key) in book' :key='key' >
              <template v-if="book_brif.hasOwnProperty(key)&&value!=null&&value!=0">
                <div class ='desc_item'>{{book_brif[key]}}:{{value}}</div>
              </template>
            </li><p/>
          </div>
        </el-col>
        <el-col class="star" :span="6">
          <el-rate
            v-model="star"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value}">
          </el-rate>
        </el-col>
      </el-card>
      <div class="desc1 author_desc" v-show="!book.author_desc==''">
        <template>
          <span class="desc2">作者简介</span><p/>
          <span class="desc2">{{book.author_desc}}</span>
        </template>
      </div>
      <p>
      <div class="desc1" v-show="!book.book_desc==''">
        <template>
          <span class="desc2">书籍简介</span><p/>
          <span class="desc2">{{book.book_desc}}</span>
        </template>
      </div>
      <p>
      <div class="desc1 review">
        <template>
          <span class="desc2">评价</span>
          <p>
          <div class="reviewitem desc2">
            <el-rate
              text-color="#ff9900"
              show-text>
            </el-rate>
            <span class="">此处是评价</span>
          </div>
        </template>
      </div>
      <div class="myview desc2">
        <span>我要评价</span>
        <el-rate
              text-color="#ff9900"
              show-text>
        </el-rate>
        <textarea height='200px' width='500px'></textarea>
      </div>
    </el-col>
    <el-col :span="8">
      <div class="tag" v-for='label in labels' :key="label">
        <el-tag type="success" size='medium'>{{label}}</el-tag>
      </div>
    </el-col>
  </el-card>
</template>

<script>
export default {
  data(){
    return{
      labels:[],
      book: {},
      book_brif: {'title':'书名','author':'作者','pub_site':'出版社','pub_time':'出版日期',isbn:'ISBN',bind:'装版',pages:'页数',price:'价格'},
      id: 0,
      star: 4.2
    }
  },
  created(){
    this.id = this.$route.params.id;
    this.getBook(this.id)
    console.log(this.book.author)
  },
  methods:{
    async getBook(id){
      const result = await this.$http.get('/api/book/'+this.id)
      if(result.status !==200)this.$message.error("网络错误")
      else{
        this.book = result.data
      }
      const la = await this.$http.get('/api/getbooklabels/?id='+this.id)
      this.labels = la.data
    }
  }
}
</script>

<style scoped>

.book_desc{
  height: 350px;
  display: block;
  float: none;
  margin-bottom: 20px;
  box-shadow: 1px 1px 10px #efefef !important
}

.desc{
  width: 210px;
  margin-top: 45px;
  float: right;
  font-size: 15px;
}

li{
  list-style: none;
}

.title{
  font-size: 20px;
}

.desc_item{
  margin-top: 8px;
}

.col1{
  text-align: center;
  height: 350px;
}

.col1 img{
  margin-top: 10px;
}

.desc1{
  margin-bottom: 20px;
  box-shadow: 1px 1px 20px #efefef
}

.desc2{
  display: block;
  padding: 5px 10px 5px 10px;
}

.tag{
  margin-left: 20px;
  width: 100px;
  float: left;
  margin-bottom: 15px;
}

.star{
  margin-left: 40px;
  margin-top: 50px;
}
</style>