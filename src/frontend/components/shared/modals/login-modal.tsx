import React from "react";
import { Modal } from "./modal";
import { Input } from "@/components/ui";
import { Button } from "@/components/ui";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h2 className="text-4xl font-bold mb-8">Вход</h2>
      <form>
        <div className="mb-4">
          <label className="block text-xl font-medium text-gray-700 p-2">Email</label>
          <Input
            type="email"
            placeholder="user@example.com"
            className="w-full p-2 border-gray-500 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-xl font-medium text-gray-700 p-2">Пароль</label>
          <Input
            type="password"
            placeholder="Введите ваш пароль"
            className="w-full p-2 border-gray-500 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <Button className="w-full mt-3 text-lg">Войти</Button>
        <Button className="w-full mt-3 bg-gray-600 text-lg">Зарегистрироваться</Button>
      </form>
    </Modal>
  );
};
