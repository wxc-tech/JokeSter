class AddPortraitToUser < ActiveRecord::Migration
  def change
    add_column :users, :portrait, :string
  end
end
