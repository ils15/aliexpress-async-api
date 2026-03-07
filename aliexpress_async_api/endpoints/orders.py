"""
Orders endpoint module
"""

from typing import List, Optional

from aliexpress_async_api.models import Order

from .base import BaseEndpoint


class OrdersEndpoint(BaseEndpoint):
    """Orders endpoint methods"""

    async def get_order_list(
        self,
        start_time: str,
        end_time: str,
        status: str = "Completed",
        page_no: int = 1,
        page_size: int = 20,
        access_token: Optional[str] = None,
    ) -> List[Order]:
        """Get list of orders"""
        api_method = "aliexpress.affiliate.order.list"
        business = {
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "page_no": str(page_no),
            "page_size": str(page_size),
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_list_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]

    async def get_order_list_by_index(
        self,
        start_query_index_id: str,
        start_time: str,
        end_time: str,
        time_type: str = "payment_time",
        status: str = "Completed",
        page_size: int = 20,
        access_token: Optional[str] = None,
    ) -> List[Order]:
        """Get orders by index"""
        api_method = "aliexpress.affiliate.order.listbyindex"
        business = {
            "start_query_index_id": str(start_query_index_id),
            "start_time": start_time,
            "end_time": end_time,
            "time_type": time_type,
            "status": status,
            "page_size": str(page_size),
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_listbyindex_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]

    async def get_order_info(
        self, order_ids: List[str], access_token: Optional[str] = None
    ) -> List[Order]:
        """Get specific order information"""
        api_method = "aliexpress.affiliate.order.get"
        business = {"order_ids": ",".join(str(i) for i in order_ids)}

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]
