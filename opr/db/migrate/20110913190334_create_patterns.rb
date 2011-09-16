class CreatePatterns < ActiveRecord::Migration
  def self.up
    create_table :patterns do |t|
      t.string :title
      t.string :slug
      t.text :description

      t.timestamps
    end
  end

  def self.down
    drop_table :patterns
  end
end
