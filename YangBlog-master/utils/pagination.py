class Page:
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
    @property
    def start(self):
        return (self.current_page-1) * self.per_page_count
    @property
    def end(self):
        return self.current_page * self.per_page_count
    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v
    def page_str(self, base_url):
        page_list = []
        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num+1)/2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num-1)/2
                end_index = self.current_page + (self.pager_num+1)/2
                if (self.current_page + (self.pager_num-1)/2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1
        page_count = '<a class="page" href="javascript:void(0);"><button type="button" class="btn btn-default">共 %s 页</button></a>' % (int(self.total_count))
        page_list.append(page_count)
        if self.current_page == 1:
            prev = '<a class="page" href="javascript:void(0);"><button type="button" class="btn btn-default" disabled>上一页</button></a>'
        else:
            prev = '<a class="page" href="%sp=%s&pre=%s"><button type="button" class="btn btn-default">上一页</button></a>' %(base_url, self.current_page-1, int(self.per_page_count))
        page_list.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<a class="page" href="%sp=%s&pre=%s"><button type="button" class="btn btn-success">%s</button></a>'%(base_url,i,int(self.per_page_count),i)
            else:
                temp = '<a class="page" href="%sp=%s&pre=%s"><button type="button" class="btn btn-default">%s</button></a>' %(base_url,i,int(self.per_page_count),i)
            page_list.append(temp)
        if self.current_page == self.total_count:
            nex = '<a class="page" href="javascript:void(0);"><button type="button" class="btn btn-default" disabled>下一页</button></a>'
        else:
            nex = '<a class="page" href="%sp=%s&pre=%s"><button type="button" class="btn btn-default">下一页</button></a>' %(base_url,self.current_page+1, int(self.per_page_count))
        page_list.append(nex)
        jump = """
       <input type='text' style='width:40px;padding: 2px;'/><a style='padding: 5px;' onclick='jumpTo(this, "%s?p=");'><button type="button" class="btn btn-info">GO</button></a>
        <script>
            function jumpTo(ths,base){
                var val = ths.previousSibling.value;
                location.href = base + val;
            }
        </script>
        """ %(base_url,)
        page_list.append(jump)
        page_str = "".join(page_list)
        return page_str