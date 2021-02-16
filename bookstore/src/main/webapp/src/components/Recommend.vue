<template>
<div>
  <el-col :span="16">
    <el-tooltip class="item" effect="dark" content="此处是根据用户习惯推荐的图书列表" placement="right">
      <el-button class="change" @click="recommend(1)" type="info" round plain>换一批</el-button>
    </el-tooltip>
    <el-card>
      <el-table :data="result.bookList" @row-click="rowClick" ref='table'>
        <el-table-column label="封面" width="120">
            <img class="img" src="../assets/imgs/tempimg.jpg">
        </el-table-column>
        <el-table-column label="书名" prop="title" width="240">
        </el-table-column>
        <el-table-column label="介绍" prop="info" width="450">
        </el-table-column>
      </el-table>
    </el-card>
  </el-col>
  <el-col :span="8">
      <div class="tag" v-for='label in labels' :key="label">
        <el-tag size='medium'>{{label}}</el-tag>
      </div>
  </el-col>
</div>
</template>

<script>
export default {
  data(){
    return{
      labels:[],
      result:{
        bookList:[],
        num:20
      }
    }
  },
  created(){
    this.recommend()
  },
  methods: {
    rowClick(row){
      console.log(row.id)
      this.$router.push({path:'/book/'+row.id})
    },
    async recommend(x){
      const token = window.sessionStorage.getItem("token")
      const result = await this.$http.get("redisapi/getrecommend?token="+token)
      this.result.bookList=result.data
      const la=await this.$http.get("api/labels")
      this.labels = la.data
      if(x==1)this.$message.success("切换成功")
    }
  }
}
</script>

<style scoped>


li{
  list-style: none;
  height: 100px !important;
}

.img{
  width: 92px;
  height: 120px;
}

.tag{
  margin-left: 13px;
  width: 80px;
  float: left;
  margin-bottom: 12px;
}
.change{
  margin-bottom: 30px;
}
</style>