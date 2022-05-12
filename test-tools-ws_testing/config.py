Host = "http://testing-mp-api.jiansutech.com"
# 盲盒id
box_id = "1524336008839352321"
# 登录
register_api = Host + "/mp/auth/appRegister"
user_detail_api = Host +"/blockbzz/product/user/detail"
# 盲盒列表
box_list_api = Host +"/mp/admin/banner/list?type=BLINDBOX_BANNER"
# 盲盒详情
box_detail_api = Host +"/blockbzz/blindbox/detail/" + box_id
# 购买盲盒
buy_box_api = Host +"/blockbzz/blindbox/create-order"
# =================================================================

# 店铺id
shop_id = "1518889855165853697"
# 店铺信息
shop_detail_api = Host +"/blockbzz/activity/shop/detail/" + shop_id
# 店铺商品列表
shop_product_list_api =Host + f"/blockbzz/activity/product/page?shopId={shop_id}"
# 店铺商品详情
shop_product_detail_api =Host +"/blockbzz/activity/product/detail/{}"
# 购买店铺内商品
buy_shop_product_api = Host +"/blockbzz/product/order/create"



