"use client";

import { Container, Filters, ProductsGroupList } from "../components/shared" 

export default function Page() {
  return(
    <main>

      {/* Основная часть сайта*/}
      <Container className="pb-14 mt-10">
        <div className="flex gap-[60px]">

          {/* Фильтрация*/}
          <div className="w-[250px]">
            <Filters/>
          </div>

          {/* Список товаров*/}
          <div className="flex-1">
            <div className=" flex flex-col gap-16">
              <ProductsGroupList 
                title="Все товары"
                items={[
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                  {
                    id: 0,
                    name: "PlayStation 5 Pro",
                    price: 68000
                  },
                ]}
              />
            </div>
          </div>
        </div>
        
      </Container>

    </main>
  )
}