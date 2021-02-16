<template>
<div>
  <el-col :span="16">
    <el-card>
      <el-table :data="result.bookList" @row-click="rowClick" ref='table'>
        <el-table-column label="封面" width="120">
          <!-- <template v-slot:default="scope"> -->
            <img class="img" src="../assets/imgs/tempimg.jpg">
          <!-- </template> -->
        </el-table-column>
        <el-table-column label="书名" prop="title" width="240">
          <!-- <li v-for="item in bookList" :key="item.id">
            <el-col :span="4"><img src='../assets/imgs/tempimg.jpg'></el-col>
            <el-col :span="8">{{item.info}}</el-col>
          </li> -->
        </el-table-column>
        <el-table-column label="介绍" prop="info" width="450">

        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="query.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="result.num"
      ></el-pagination>
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
      query:{
        key:'',
        page:1,
        pagesize:10
      },
      result:{
        bookList:[],
        num:10
      },
      
    }
  },
  created(){
    this.query.key = this.$route.params.key
    this.search()
  },
  methods: {
    async search(){
      const res = await this.$http.get('api/tag',{params:this.query})
      this.result.bookList=res.data.data
      this.result.num=res.data.num
      const la=await this.$http.get("api/labels")
      this.labels = la.data
    },
    handleSizeChange(newsize){
      this.query.pagesize=newsize
      this.search()
    },
    handleCurrentChange(current){
      this.query.page=current
      this.search()
    },
    rowClick(row){
      console.log(row.id)
      this.$router.push({path:'/book/'+row.id})
    }
  },
  watch:{
      '$route' (to, from) {
      this.key = this.$route.params.key
      this.search()
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
</style>