<template>
  <div class="app-container">
    <el-form ref="form" :inline="true" :model="form" label-width="80px">
      <el-form-item label="关键词">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="房屋用途">
        <el-select v-model="form.use" placeholder="请选择房屋用途">
          <el-option label="普通住宅" value="普通住宅"></el-option>
          <el-option label="商住两用" value="商住两用"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="装修情况">
        <el-select v-model="form.decorate" placeholder="请选择装修情况">
          <el-option label="精装" value="精装"></el-option>
          <el-option label="简装" value="简装"></el-option>
          <el-option label="毛坯" value="毛坯"></el-option>
          <el-option label="其他" value="其他"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="面积范围">
        <el-input v-model="form.min_size"></el-input>
      </el-form-item>
      <el-form-item label=":">
        <el-input v-model="form.max_size"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchData">搜索</el-button>
        <el-button @click="clearForm">清空</el-button>
      </el-form-item>
    </el-form>
    <el-table
      v-loading="listLoading"
      :data="houseList.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column label="标题" align="center">
        <template slot-scope="scope">
          <el-link target="_blank" type="primary" :href="scope.row.url">{{ scope.row.title }}</el-link>
        </template>
      </el-table-column>
      <el-table-column label="地区" align="center">
        <template slot-scope="scope">
          {{ scope.row.area }}
        </template>
      </el-table-column>
      <el-table-column label="小区" align="center">
        <template slot-scope="scope">
          {{ scope.row.community }}
        </template>
      </el-table-column>
      <el-table-column label="价格（万元）" align="center">
        <template slot-scope="scope">
          {{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column label="房型" align="center">
        <template slot-scope="scope">
          {{ scope.row.layout }}
        </template>
      </el-table-column>
      <el-table-column label="大小（平米）" align="center">
        <template slot-scope="scope">
          {{ scope.row.size }}
        </template>
      </el-table-column>
      <el-table-column label="朝向" align="center">
        <template slot-scope="scope">
          {{ scope.row.toward }}
        </template>
      </el-table-column>
      <el-table-column label="装修">
        <template slot-scope="scope">
          {{ scope.row.decorate }}
        </template>
      </el-table-column>
      <el-table-column label="楼层">
        <template slot-scope="scope">
          {{ scope.row.layer }}
        </template>
      </el-table-column>
      <el-table-column label="挂牌时间">
        <template slot-scope="scope">
          {{ scope.row.year }}
        </template>
      </el-table-column>
      <el-table-column label="交易权属">
        <template slot-scope="scope">
          {{ scope.row.type }}
        </template>
      </el-table-column>
      <el-table-column label="房屋用途">
        <template slot-scope="scope">
          {{ scope.row.use }}
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5, 10, 20, 40]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="houseList.length">  /*每页显示多少条数据*/
    </el-pagination>
  </div>
</template>

<script>
import {getHouseList} from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      listLoading: true,
      form: {
        gearbox: '',
        title: '',
        age: '',
        gearbox_type: '',
        max_price: '',
        min_price: '',
        min_size: '',
        max_size: ''
      },
      currentPage: 1,
      pagesize: 10,
      houseList: []
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    // 初始页currentPage、初始每页数据数pagesize和数据data
    handleSizeChange: function(size) {
      this.pagesize = size
    },
    handleCurrentChange: function(currentPage) {
      this.currentPage = currentPage
    },
    handleUserList() {

    },
    clearForm() {
      this.form = {
        title: '',
        age: '',
        gearbox_type: '',
        max_price: '',
        min_price: '',
        max_size: '',
        min_size: ''
      }
    },
    fetchData() {
      this.listLoading = true
      getHouseList(this.form).then(response => {
        this.houseList = response.datas
        this.listLoading = false
      })
    }
  }
}
</script>
