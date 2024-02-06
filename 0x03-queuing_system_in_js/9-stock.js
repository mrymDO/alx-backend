import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const clientGet = promisify(client.get).bind(client);
const clientSet = promisify(client.set).bind(client);

const listProducts = [
    { Id: 1, name: "Suitcase 250", price: 50, stock: 4 },
    { Id: 2, name: "Suitcase 450", price: 100, stock: 10 },
    { Id: 3, name: "Suitcase 650", price: 350, stock: 2 },
    { Id: 4, name: "Suitcase 1050", price: 550, stock: 5 }
];

function getItemById(id) {
    return listProducts.find(item => item.Id === id);
}

async function reserveStockById(itemId, stock) {
    await clientSet(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
    const stock = await clientGet(itemId);
    return parseInt(stock) || 0;
}

app.get('/list_products', (req, res) => {
    res.json(listProducts.map(item => ({
        itemId: item.Id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock
    })));
});

app.get('/list_products/:itemId', async (req, res) => {
    const id = Number(req.params.itemId);
    const item = getItemById(id);
    const reservedStock = await getCurrentReservedStockById(id);

    if (item) {
        const currentQuantity = item.stock - reservedStock;
        res.json({
            itemId: item.Id,
            itemName: item.name,
            price: item.price,
            initialAvailableQuantity: item.stock,
            currentQuantity: currentQuantity
        });
    } else {
        res.status(404).json({ status: "Product not found" });
    }
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const id = Number(req.params.itemId);
    const item = getItemById(id);

    if (!item) {
        res.status(404).json({ status: "Product not found" });
        return;
    }

    const stock = await getCurrentReservedStockById(id);
    const currentQuantity = item.stock - stock;

    if (currentQuantity < 1) {
        res.json({ status: "Not enough stock available", itemId: id });
    } else {
        reserveStockById(id, stock + 1);
        res.json({ status: "Reservation confirmed", itemId: id });
    }
});

app.listen(1245, () => {
    console.log('Server is running on port 1245');
});
