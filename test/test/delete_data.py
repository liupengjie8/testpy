
# -- 数据准备
# prepare_index_value_result
# prepare_index_value_status
# stuff_source_relation
# prepare_proof_stuff
# -- 平台报送
# perf_index_fill
# perf_index_fill_detail
# perf_fill_work
# nation_performance_time
# perf_fill_detial_update_rec
# perf_index_qc_result

tables = ['perf_index_fill', 'perf_index_fill_detail', 'perf_fill_work', 'nation_performance_time',
          'perf_fill_detial_update_rec', 'perf_index_qc_result']
for table in tables:
    print('create table '+table+'_bak_07221622 as select * from '+table+';')
for table in tables:
    print('delete from '+table+';')