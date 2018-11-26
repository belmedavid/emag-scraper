from quart import Quart, render_template, request, redirect
import data_manager
import time
import scraping


app = Quart(__name__)


@app.route("/")
async def index():
    table_names = data_manager.get_table_names()
    table = data_manager.get_table_name(request.args.get('table_name'))
    order_by = data_manager.get_order_by(request.args.get('order_by'))
    order_direction = data_manager.get_order_direction(request.args.get('order_direction'))
    ordered_products = data_manager.get_ordered_products(table, order_by, order_direction)
    if request.args.get('search'):
        search = '%' + request.args.get('search') + '%'
        ordered_products = data_manager.get_searched_product_names(table, search)

    return await render_template('index.html', ordered_products=ordered_products, order_by=order_by,
                                 table_names=table_names)


@app.route("/start-scrap")
async def start_scrap():
    while True:

        next_time = time.time() + 15
        await scraping.scraping()
        wait_for = next_time - time.time()
        if wait_for > 0:
            time.sleep(wait_for)

    scraping.scraping().close()

@app.route("/stop-scrap")
async def stop_scrap():
    scraping.scraping().close()

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=False)
