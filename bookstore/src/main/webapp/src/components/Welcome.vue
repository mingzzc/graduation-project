<template>
  <el-card class="welcome">
    <el-col :span="16" class="bookArea">
      <ul>
        <li v-for="book in booksList" :key="book.id">
          <div class = 'cover'>
              <el-tooltip class="item" effect="dark" :content="book.info" placement="top ">
                <router-link :to="'/book/'+book.id">
                  <img :href="'/book/'+book.id" width="120px" height="150px" :src='"../assets/imgs/tempimg.jpg"'>
                  <div>{{book.title}}</div>
                </router-link>
              </el-tooltip>
          </div>
        </li>
      </ul>
    </el-col>
    <el-col :span="8" class="tagArea">标签:<p/>
      <div class="tag" v-for='label in labels' :key="label">
        <el-tag size='medium'>{{label}}</el-tag>
      </div>
    </el-col>
  </el-card>
</template>

<script>
export default {
   data() {
    return {
      booksList: [],
      labels: []
    }
  
  },
  created() {
    this.getBooksList();
    this.init()
  },
  methods: {
    async getBooksList(){
      const result = await this.$http.get('api/books',{params:{num:20}})
      if(result.status !==200)console.log('请求失败')
      else{
        const res = result.data
        this.booksList = res
      }
      const la=await this.$http.get("api/labels")
      this.labels = la.data
    }
  }
}
</script>

<style scoped>

.bookArea{
  background-color: rgb(250, 250, 250);
}

li{
  float: left;
  list-style: none;
  margin: 3px 8px;
  height: 200px;
  width: 130px;
}

.cover {
  text-align: center;
  text-decoration: none;
}

.cover a:link{
  text-decoration: none !important;
  font-size: small;
}

.tag{
  margin-left: 13px;
  width: 80px;
  float: left;
  margin-bottom: 12px;
}
</style>