<template>
  <div class="app-container">
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="是否有电梯">
        <el-select v-model="formInline.elevator" placeholder="">
          <el-option label="是" value="1"></el-option>
          <el-option label="否" value="0"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="选择行政区">
        <el-select v-model="formInline.region" placeholder="">
          <el-option label="花山区" value="花山区"></el-option>
          <el-option label="雨山区" value="雨山区"></el-option>
          <el-option label="当涂县" value="当涂县"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="面积">
        <el-input v-model="formInline.area" placeholder=""></el-input>
      </el-form-item>
      <el-form-item label="装修情况">
        <el-select v-model="formInline.decorate" placeholder="">
          <el-option label="简装" value="简装"></el-option>
          <el-option label="毛坯" value="毛坯"></el-option>
          <el-option label="精装" value="精装"></el-option>
          <el-option label="其他" value="其他"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="建造年份">
        <el-input v-model="formInline.year" placeholder=""></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="start">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="update">更新训练集</el-button>
      </el-form-item>
    </el-form>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>预测条件</span>
      </div>
      <div class="text item">
        <span>是否有电梯: </span>
        <span v-if="formInline.elevator === '1'">是</span>
        <span v-if="formInline.elevator === '0'">否</span><br>
        <span>所在行政区: </span>{{formInline.region}}<br>
        <span>面积: </span>{{formInline.area}} (平方米)<br>
        <span>装修情况: </span>{{formInline.decorate}}<br>
        <span>建造年份: </span>{{formInline.year}} 年造<br>
      </div>
    </el-card>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>预测结果</span>
      </div>
      <div class="text item">
        <span>房价: {{this.price}}</span>（万元）<br>
      </div>
    </el-card>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import {predict, updatePredictResult} from '@/api/house'

export default {
  data() {
    return {
      logs: [],
      price: '',
      formInline: {
        elevator: '', // 电梯
        region: '', // 地区
        area: '', // 面积
        year: '', // 年份
        decorate: '' // 装修
      }
    }
  },
  mounted() {

  },
  beforeDestroy() {
    this.clearRequestTimer()
  },
  methods: {
    start() {
      predict(this.formInline).then((resp) => {
        console.log(resp)
        this.price = resp.data
        this.$message.success('预测完成！')
      })
    },
    update() {
      this.$message.info('即将进行训练，过程需要较长一段时间，预测成功后有提示！')
      updatePredictResult().then((resp) => {
        console.log(resp)
        this.$message.success('更新成功！')
      })
    }
  }
}
</script>

<style scoped>
.line {
  text-align: center;
}
</style>

