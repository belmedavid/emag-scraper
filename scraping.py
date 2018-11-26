import data_manager
from requests_html import AsyncHTMLSession
import datetime
import pyppeteer
from pyppeteer import errors


async def scraping():
    unix_time = datetime.datetime.now()
    table = str(unix_time)[:7]
    actual_items_list = []
    product_names_in_database = data_manager.get_all_product_name(table)
    product_name_list = []
    checker_names_in_database = data_manager.get_all_checker_name()
    checker_list = []
    try:
        asession = AsyncHTMLSession()
        req = await asession.get('https://www.emag.hu/homepage')
        await req.html.arender()

        cards = req.html.find('.js-card-item')
        for product in product_names_in_database:
            product_name_list.append(product['product_name'])

        for product in checker_names_in_database:
            checker_list.append(product['name'])

        for item in cards:
            if 'data-name' and 'data-url' in item.attrs:
                name = item.attrs['data-name']
                link = item.attrs['data-url']
                if 'live_asp' in link:
                    price = item.find('.product-new-price')[0].text[:-3].replace('.', '')
                    living_link = repr(item.find('.card')[0].absolute_links).strip("'{}")
                    actual_items_list.append(name)
                    if name not in checker_list:
                        data_manager.add_product_to_checker(name)
                        if name not in product_name_list:
                            row = (name, price, unix_time, living_link, 1)
                            data_manager.add_product_to_products(table, row)
                        else:
                            updated_quantity = {}
                            quantity = data_manager.get_quantity_by_name(table, name)
                            updated_quantity['quantity'] = quantity['quantity'] + 1
                            data_manager.update_product_quantity_by_name(table, name, price, unix_time,
                                                                         updated_quantity)
        if actual_items_list:
            for checked_item in checker_list:
                if checked_item not in actual_items_list:
                    data_manager.remove_product_from_checker(checked_item)
            actual_items_list.clear()
        else:
            act_time = str(unix_time)[:19]
            print(act_time, 'The recently bought list is empty!')
        req.close()
        await asession.close()
    except (ConnectionError, pyppeteer.errors.NetworkError) as e:

        print(e)
        pass
    except pyppeteer.errors.NetworkError:
        print('exit')
        scraping().close()

